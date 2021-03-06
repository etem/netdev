import asyncio
import logging

import yaml

import netdev

config_path = 'config.yaml'

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
netdev.logger.setLevel(logging.DEBUG)


async def task(param):
    async with netdev.create(**param) as routeros:
        commands = ['/ip address', 'print', '/']
        for cmd in commands:
            print(await routeros.send_command(cmd))
        out = await routeros.send_config_set(commands)
        print(out)


async def run():
    config = yaml.load(open(config_path, 'r'))
    devices = yaml.load(open(config['device_list'], 'r'))
    params = [p for p in devices if p['device_type'] == 'mikrotik_routeros']
    tasks = []
    for param in params:
        tasks.append(task(param))
    await asyncio.wait(tasks)


loop = asyncio.get_event_loop()
loop.run_until_complete(run())
