import sys, os
import app.lib.common.rootvar as root

#FIXME! The __ROOTEXEDIR__ was not working, so it need to be fixed!! the module was not called!

def main(path,opath,dbtype, dbname, g, rid):
    # blastdb
    g.db.execute('UPDATE reference SET status="making blast db" WHERE reference_id="'+rid+'"')
    g.db.commit()
    finput=path+'/'+dbname
    output=opath+'/'+'nr'
    exe="/home/raid/www/MetaStorm/main/Files/bin/makeblastdb" #root.__ROOTEXEDIR__+"/makeblastdb";
    options="-max_file_sz 10000000000000"
    dbtype=dbtype
    cmd=" ".join([exe, '-in', finput, '-out', output, '-dbtype', dbtype])
    status=os.system(cmd)
    g.db.execute('UPDATE reference SET status="making diamond db" WHERE reference_id="'+rid+'"')
    g.db.commit()
    output=opath+'/'+'dataset.diamond'
    exe="/home/raid/www/MetaStorm/main/Files/bin/diamond makedb"   #root.__ROOTEXEDIR__+"/diamond makedb"
    cmd=" ".join([exe, '--in', finput, '-d', output])
    status=os.system(cmd)
    if dbtype=="nucl":
        g.db.execute('UPDATE reference SET status="making bowtie2 db" WHERE reference_id="'+rid+'"')
        g.db.commit()
        output=opath+'/'+'dataset'
        exe="/home/raid/www/MetaStorm/main/Files/bin/bowtie2-build"  #root.__ROOTEXEDIR__+"/bowtie2-build"
        cmd=" ".join([exe, finput, output])
        status=os.system(cmd)

    return status
