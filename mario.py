from os import pipe
from GenerationPipeline import GenerationPipeline


class Mario(GenerationPipeline):
    def __init__(self):
        self.game_process_command = ['java', '-jar', 'mario_simulator.jar', 'NO_FLAW']



if __name__ == '__main__':
    pipeline = Mario()
    pipeline.run()
    pipeline.build_flawed_agents_links()
