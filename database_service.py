 
from datetime import datetime, timedelta, timezone
from typing import Callable, List

from mongita import MongitaClientDisk
from mongita.database import Database
from mongita.collection import Collection

from bson import ObjectId

# Handle races as object of data points
# Be able to load only race metadata (start/end time, etc) without loading data points

class DataCallback():
    def __init__(self, module_name: str, function: Callable) -> None:
        self.module_name = module_name
        self.exec = function

class Database_Service():
    def __init__(self, db_name: str) -> None:
        self.name = db_name
        self._db_client = MongitaClientDisk(".mongita")
        self._db: Database = eval(f"self._db_client.{db_name}")

        self._callbacks: List[DataCallback] = []

    def _run_callbacks(self, module_name: str, data: dict):
        for cbk in self._callbacks:
            if module_name in cbk.module_name:
                cbk.exec(data)

    def register_callback(self, target_name: str, callback: Callable):
            self._callbacks.append(DataCallback(target_name, callback))

        #if not any(
        #    ((target_name in cbk.module_name) and (callback == cbk.exec)) 
        #    for cbk in self._callbacks
        #):

    # Leaving the target empty will unregister the callback from all the targets.
    # Leaving the callback empty will unregister all the callbacks from the target.
    def unregister_callback(self, target_name: str = None, callback: Callable = None):
        for idx, cbk in enumerate(self._callbacks):
            rm_t = False
            rm_c = False

            if not target_name is None:
                if target_name == cbk.module_name:
                    rm_t = True
            else:
                rm_t = True

            if callback is None:
                if callback == cbk.exec:
                    rm_c = True
            else:
                rm_c = True

            if (rm_t and rm_c):
                self._callbacks.pop(idx)

    def insert_data(self, module_name: str, data: dict):
        coll: Collection = eval(f"self._db.{module_name}")
        coll.insert_one(data)

        self._run_callbacks(module_name, data)
    
    # from_date has to be further in time than to_date. Ex: from 25/02/2022 to 30/02/2022
    # Defaults to data up to this instant if only from is provided.
    def obtain_data(self, module_name: str, from_date: datetime, to_date: datetime = datetime.now()):
        from_id = ObjectId.from_datetime(from_date.astimezone(timezone.utc))
        to_id = ObjectId.from_datetime(to_date.astimezone(timezone.utc))
        time_range_filter = {
            "_id": {
                "$gt": from_id,
                "$lte": to_id
            }
        }

        coll: Collection = eval(f"self._db.{module_name}")
        return list(coll.find(time_range_filter))

        