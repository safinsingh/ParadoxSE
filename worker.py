from engine import ParadoxSE

worker = ParadoxSE("config.yml")
config = worker.parse()
worker.update()
