import subprocess
import yaml
from typing import Final, List, Callable
from test_plan import TestPlan
import json
import sys

def main():
    runners_path = sys.argv[1]
    proc: Final[subprocess.CompletedProcess] = subprocess.run(
        f'find {runners_path} -name "*.yml"',
        shell=True, stdout=subprocess.PIPE, text=True
    )
    test_plans: Final[List[TestPlan]] = []
    for file in [x for x in proc.stdout.split('\n') if len(x) > 0]:
        with open(file) as f:
            test_plans.append(TestPlan.create(yaml.safe_load(f)))
    map_handler: Callable[[TestPlan], dict] = lambda x: x.dict
    sys.stdout.write(json.dumps(list(map(map_handler, test_plans))))

if __name__ == '__main__':
    main()
