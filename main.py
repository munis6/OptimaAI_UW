from optimaai_uw.core.DAG_orchestrator import DAGOrchestrator

def main():
    # raw_json can be empty — IntakeAgent will replace it
    raw_json = {}

    orchestrator = DAGOrchestrator()
    final_json = orchestrator.execute(raw_json)

    print("\n\n===== FINAL JSON OUTPUT =====")
    print(final_json)

if __name__ == "__main__":
    main()
