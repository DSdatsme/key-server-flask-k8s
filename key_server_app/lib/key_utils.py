from constants import KEY_NOT_FOUND_MESSAGE, KEY_NOT_FOUND_STATUS_CODE

def is_key_present(all_keys, req_key):
  if req_key in all_keys.keys():
    return all_keys[req_key]
  else:
    raise Exception(KEY_NOT_FOUND_MESSAGE.format(req_key), KEY_NOT_FOUND_STATUS_CODE)

def search_key_by_prefix(all_keys, search_str):
  return [each_key for each_key in all_keys if each_key.startswith(search_str)]

def search_key_by_suffix(all_keys, search_str):
  return [each_key for each_key in all_keys if each_key.endswith(search_str)]
