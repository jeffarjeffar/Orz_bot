import asyncio

async def run(cmd):
    proc = await asyncio.create_subprocess_shell(cmd, stdout=asyncio.subprocess.PIPE,
                                                 stderr=asyncio.subprocess.PIPE)

    stdout, stderr = await proc.communicate()

    stdout = str(stdout, 'utf-8')
    stderr = str(stderr, 'utf-8')

    # print(f'Done running {cmd}\n{stdout}\n{stderr}')
    
    return proc.returncode, stdout, stderr

async def time(cmd, time_limit):
    # print('Timing', cmd)
    try:
        return await asyncio.wait_for(run(cmd), timeout=time_limit)
    except asyncio.TimeoutError:
        return None