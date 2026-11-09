.PHONY: help doctor bench v0 v1 v2 observe learn build build-v2 test report demo ablate reset clean
.DEFAULT_GOAL := help

PY ?= python3

help:  ## muestra esta ayuda
	@echo ""
	@echo "  Corre SIEMPRE desde la raiz del repo (donde esta este Makefile)."
	@echo "  No hay dependencias que instalar: todo es stdlib de Python."
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN{FS=":.*?## "}{printf "  \033[1m%-12s\033[0m %s\n", $$1, $$2}'
	@echo ""

doctor:  ## revisa que todo este en su lugar antes de empezar
	@echo ""
	@echo "  directorio actual : $(CURDIR)"
	@test -f Makefile -a -d bench -a -d agents \
	  && echo "  raiz del repo     : OK" \
	  || echo "  raiz del repo     : MAL -> haz 'cd' a la carpeta que contiene el Makefile"
	@printf "  python3           : "; command -v $(PY) >/dev/null && $(PY) --version || echo "FALTA"
	@printf "  make              : "; command -v make >/dev/null && echo "OK" || echo "FALTA (instala Xcode CLT)"
	@printf "  banco de casos    : "; test -f bench/cases.jsonl \
	  && echo "$$(wc -l < bench/cases.jsonl | tr -d ' ') casos" || echo "falta -> corre 'make bench'"
	@printf "  lecciones         : "; test -s lessons/lessons.jsonl \
	  && echo "$$(wc -l < lessons/lessons.jsonl | tr -d ' ') aprendidas" || echo "0 (normal al empezar)"
	@printf "  agentes           : "; ls -d agents/v* 2>/dev/null | tr '\n' ' '; echo
	@printf "  codex (opcional)  : "; command -v codex >/dev/null && codex --version || echo "no instalado"
	@printf "  claude (opcional) : "; command -v claude >/dev/null && echo "OK" || echo "no instalado"
	@printf "  openai (opcional) : "; $(PY) -c "import openai" 2>/dev/null \
	  && echo "OK" || echo "no instalado (NO hace falta: el motor stub es determinista)"
	@echo ""
	@echo "  Para empezar:  make demo"
	@echo ""

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

# Los tests en ROJO son el estado ESPERADO antes de `make build`, asi que este
# target no debe abortar make. El `|| echo` evita el "make: *** Error 1" que
# parece una falla del proyecto cuando en realidad es la medicion correcta.
test:  ## corre los tests de las lecciones: make test AGENT=v2 [L=L3]
	@RSI_AGENT=$(or $(AGENT),v1) $(PY) run_tests.py $(L) \
	  || echo "  ^ tests en ROJO. Antes de 'make build' esto es CORRECTO: el sucesor todavia no existe."

ablate:  ## apaga una leccion y mide: make ablate L=L2 V=v2
	$(PY) agents/run.py --version $(or $(V),v2) --split holdout --ablate $(L)
	$(PY) bench/score.py runs/$(or $(V),v2)-ablate-$(L)-holdout.json

report:  ## tabla comparativa de todas las versiones
	$(PY) report.py --split holdout

demo:  ## secuencia completa para la presentacion
	@$(MAKE) bench v0 observe learn report

clean:  ## borra corridas (NO borra lecciones ni casos)
	rm -f runs/*.json runs/*.md

reset:  ## vuelve al punto de partida para ensayar la demo desde cero
	@echo "  Esto borra: corridas, lecciones aprendidas, tests generados y V1/V2."
	@echo "  NO borra el banco de casos ni V0."
	rm -f runs/*.json runs/*.md
	rm -f tests/test_lesson_*.py
	: > lessons/lessons.jsonl
	rm -rf agents/v1 agents/v2 agents/common/tools/*.py
	touch agents/common/tools/__init__.py
	@echo "  Listo. Ahora: make demo"
