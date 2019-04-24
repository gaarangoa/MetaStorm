import sys, os
import app.lib.common.rootvar as root
import logging

log = logging.getLogger()


def main(path, opath, dbtype, dbname, g, rid):
    # blastdb
    g.db.execute(
        'UPDATE reference SET status="making blast db" WHERE reference_id="' + rid + '"'
    )
    g.db.commit()
    finput = path + "/" + dbname
    output = opath + "/" + "nr"
    exe = "/src/Files/bin/makeblastdb"  # root.__ROOTEXEDIR__+"/makeblastdb";
    options = "-max_file_sz 10000000000000"
    dbtype = dbtype
    cmd = " ".join([exe, "-in", finput, "-out", output, "-dbtype", dbtype])
    status = os.system(cmd)
    g.db.execute(
        'UPDATE reference SET status="making diamond db" WHERE reference_id="'
        + rid
        + '"'
    )
    g.db.commit()
    log.info(exe)

    output = opath + "/" + "dataset.diamond"
    exe = "/src/Files/bin/diamond makedb"  # root.__ROOTEXEDIR__+"/diamond makedb"
    cmd = " ".join([exe, "--in", finput, "-d", output])
    status = os.system(cmd)
    log.info(exe)
    if dbtype == "nucl":
        g.db.execute(
            'UPDATE reference SET status="making bowtie2 db" WHERE reference_id="'
            + rid
            + '"'
        )
        g.db.commit()
        output = opath + "/" + "dataset"
        exe = "/src/Files/bin/bowtie2-build"  # root.__ROOTEXEDIR__+"/bowtie2-build"
        cmd = " ".join([exe, finput, output])
        status = os.system(cmd)
        log.info(exe)

    return status
