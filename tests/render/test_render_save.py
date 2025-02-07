'''Manual test for render client connectivity'''

if __name__ == '__main__':
  import time
  import random
  import nmmo

  # pylint: disable=import-error
  from nmmo.render.render_client import WebsocketRenderer
  from tests.testhelpers import ScriptedAgentTestConfig

  TEST_HORIZON = 100
  RANDOM_SEED = random.randint(0, 9999)

  # config.RENDER option is gone,
  # RENDER can be done without setting any config
  config = ScriptedAgentTestConfig()
  env = nmmo.Env(config)

  env.reset(seed=RANDOM_SEED)

  # the renderer is external to the env, so need to manually initiate it
  renderer = WebsocketRenderer(env.realm)

  for tick in range(TEST_HORIZON):
    env.step({})
    renderer.render_realm()
    time.sleep(1)

  # save the packet: this is possible because config.SAVE_REPLAY = True
  env.realm.save_replay(f'replay_seed_{RANDOM_SEED:04d}.json', compress=False)
