import datetime

# Generate unique material ref key
def gen_ref_key(tbl, type):
    count = tbl.query.count()
    count += 1
    return type+str(count)+'-'+datetime.datetime.now().strftime('%y%m%d')


