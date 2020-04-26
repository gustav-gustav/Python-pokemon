import pokepy, os
client = pokepy.V2Client(cache='in_disk', cache_location=os.path.join(os.getcwd(), 'data'))
