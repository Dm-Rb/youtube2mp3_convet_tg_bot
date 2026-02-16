import os
import datetime
from asyncio import sleep

"""
Sometimes errors occur during ffmpg operation, the processing flow is interrupted, and the file path is not passed down 
the chain to the temporary file deletion handler. As a result, files accumulate on disk. This module deletes temporary 
files that were created more than 1 hour ago.
"""


async def remove_tmp_files(dirpath='downloads', timedelta_hours=1):
    if not os.path.exists(dirpath):
        return None
    datetime_now = datetime.datetime.now()
    timedelta = datetime.timedelta(hours=timedelta_hours)
    for filename in os.listdir(dirpath):
        stats = os.stat(os.path.join(dirpath, filename))
        ctime = datetime.datetime.fromtimestamp(stats.st_ctime)
        if datetime_now - ctime >= timedelta:
            try:
                # remove
                os.remove(os.path.join(dirpath, filename))
            except Exception as _ex:
                pass


async def trash_scheduler():
    while True:
        await sleep(3600)
        try:
            await remove_tmp_files()
        except Exception as e:
            pass