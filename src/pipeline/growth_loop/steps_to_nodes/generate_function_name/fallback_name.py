def fallback_name(semantic):

    return "node_" + str(abs(hash(semantic)))[:8]
