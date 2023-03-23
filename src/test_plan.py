from typing import Final, List, Dict, Callable, Optional, cast, Union

YamlTestPlanStep = Union[Dict[str, str], str]

class TestPlanStep:
    action: Final[str]
    param: Final[str]

    def __init__(self, action: str, param: str):
        self.action = str(action)
        self.param = str(param)

    @property
    def dict(self) -> Dict[str, str]:
        ret: Final[Dict[str, str]] = {
            'action': self.action,
        }
        if len(self.param) > 0:
            ret['param'] = self.param
        return ret

class TestPlan:
    device: Final[str]
    os_version: Final[str]
    languages: Final[List[str]]
    system_navigation: Final[Optional[str]]
    step_wait_time: Final[Optional[float]]
    steps: Final[List[TestPlanStep]]

    def __init__(
        self,
        device: str,
        os_version: str,
        languages: List[str],
        system_navigation: Optional[str],
        step_wait_time: Optional[float],
        steps: List[TestPlanStep]
    ):
        self.device = device
        self.os_version = os_version
        self.languages = languages
        self.system_navigation = system_navigation
        self.step_wait_time = step_wait_time
        self.steps = steps

    @staticmethod
    def validate(
        device: str,
        os_version: str,
        languages: List[str],
        step_wait_time: Optional[float],
        steps: List[YamlTestPlanStep]
    ):
        if len(device) == 0:
            raise ValueError('Required device.')
        if len(os_version) == 0:
            raise ValueError('Required os-version.')
        if len(languages) == 0:
            raise ValueError('Required languages.')
        if step_wait_time is not None and (0 > step_wait_time or step_wait_time > 3600):
            raise ValueError('Invalid step-wait-time. This is up to 3600 seconds.')
        if len(steps) == 0:
            raise ValueError('Required steps.')

    @staticmethod
    def convert_test_plan_steps(step: YamlTestPlanStep) -> TestPlanStep:
        if isinstance(step, str) is True:
            return TestPlanStep(step, "")
        elif isinstance(step, dict) is True:
            for action in filter(lambda x: x != "name", step.keys()):
                return TestPlanStep(action, step[action])
        else:
            raise ValueError('Invalid steps')

    @staticmethod
    def create(obj: any) -> 'TestPlan':
        device: Final[str] = str(obj['device'])
        os_version: Final[str] = str(obj['os-version'])
        languages: Final[List[str]] = obj['languages']
        system_navigation: Final[Optional[str]] = obj.get('system-navigation')
        step_wait_time: Final[Optional[float]] = obj.get('step-wait-time')
        steps: Final[List[YamlTestPlanStep]] = obj['steps']
        TestPlan.validate(device, os_version, languages, step_wait_time, steps)

        test_plan_steps: List[TestPlanStep] = list(map(TestPlan.convert_test_plan_steps, steps))
        return TestPlan(
            device, os_version, languages,
            system_navigation, step_wait_time, test_plan_steps
        )

    @property
    def dict(self) -> Dict:
        map_handler: Callable[[TestPlanStep], Dict] = lambda x: x.dict
        ret: Dict = {
            'device': self.device,
            'osVersion': self.os_version,
            'languages': self.languages,
            'steps': list(map(map_handler, self.steps)),
        }
        if self.system_navigation is not None:
            ret['systemNavigation'] = cast(str, self.system_navigation)
        if self.step_wait_time is not None:
            ret['stepWaitTime'] = cast(float, self.step_wait_time)
        return ret
