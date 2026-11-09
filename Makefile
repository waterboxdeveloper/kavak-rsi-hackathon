.PHONY: help bench v0 v1 v2 observe learn build build-v2 test report demo ablate clean
.DEFAULT_GOAL := help

PY ?= python3

help:  ## muestra esta ayuda
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN{FS=":.*?## "}{printf "  \033[1m%-12s\033[0m %s\n", $$1, $$2}'

bench:  ## genera el banco de 60 casos (semilla fija)
	$(PY) bench/generate_cases.py

v0:  ## corre V0 y lo califica
	$(PY) agents/run.py --version v0 --split all
	$(PY) bench/score.py runs/v0-all.json
	$(PY) agents/run.py --version v0 --split train
	$(PY) agents/run.py --version v0 --split holdout
	$(PY) bench/score.py runs/v0-holdout.json

observe:  ## paso 1: agrupa las fallas de V0 (solo train)
	$(PY) loop/observe.py runs/v0-train.json

learn:  ## paso 2: convierte fallas en lecciones + tests rojos
	$(PY) loop/learn.py runs/v0-train.failures.json

build:  ## paso 3: Codex construye V1 desde V0 + lecciones
	$(PY) loop/build.py --from v0 --to v1

v1:  ## corre V1 y lo califica
	$(PY) agents/run.py --version v1 --split holdout
	$(PY) bench/score.py runs/v1-holdout.json

observe-v1:  ## observa las fallas que quedan en V1 (train)
	$(PY) agents/run.py --version v1 --split train
	$(PY) loop/observe.py runs/v1-train.json
	$(PY) loop/learn.py runs/v1-train.failures.json

build-v2:  ## Codex construye V2 desde V1 + lecciones acumuladas
	$(PY) loop/build.py --from v1 --to v2

v2:  ## corre V2 y lo califica
	$(PY) agents/run.py --version v2 --split holdout
	$(PY) bench/score.py runs/v2-holdout.json

test:  ## corre los tests de las lecciones: make test AGENT=v2 [L=L3]
	RSI_AGENT=$(or $(AGENT),v1) $(PY) run_tests.py $(L)

ablate:  ## apaga una leccion y mide: make ablate L=L2 V=v2
	$(PY) agents/run.py --version $(or $(V),v2) --split holdout --ablate $(L)
	$(PY) bench/score.py runs/$(or $(V),v2)-ablate-$(L)-holdout.json

report:  ## tabla comparativa de todas las versiones
	$(PY) report.py --split holdout

demo:  ## secuencia completa para la presentacion
	@$(MAKE) bench v0 observe learn report

clean:  ## borra corridas (NO borra lecciones ni casos)
	rm -f runs/*.json runs/*.md
