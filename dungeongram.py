from GenerationPipeline import GenerationPipeline

class DungeonGram(GenerationPipeline):
    def __init__(self):
        pass



if __name__ == '__main__':
    pipeline = DungeonGram()
    pipeline.run()
    pipeline.build_flawed_agents_links()
    