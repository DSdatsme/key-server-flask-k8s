
def is_key_present(all_keys, req_key):
  if req_key in all_keys.keys():
    return all_keys[req_key]
  else:
    raise Exception(f"Key with ID {req_key} could not be found", 404)

def search_key_by_prefix(all_keys, search_str):
  return [each_key for each_key in all_keys if each_key.startswith(search_str)]

def search_key_by_suffix(all_keys, search_str):
  return [each_key for each_key in all_keys if each_key.endswith(search_str)]
