import re
from typing import List

message = "!wn_search a b"
if re.fullmatch("!wn_search(\s((?!th.)\w+))+(\sth=-?\d+\.\d+)?", message.lower()):
    
    th: str = message.content.lower().split("th=")[-1] if len(message.lower().split("th=")) > 1 else None
    
    if th:
        if -1 <= float(th) <= 1:
            text = " ".join(message.lower().split("th=")[:-1])
            search_values = " ".join(
                text.split(" ")[1::]
            ).strip()
            results = local_search(search_values, (float(th) + 1) / 2)

        else:
            search_values = " ".join(
                message.content.lower().split(" ")[1::]
            )
            results = local_search(search_values)
    
# [th=\d]?