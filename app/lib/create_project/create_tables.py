import sqlite3 as sql
import app.lib.common.rootvar as root

def create_tables():
    conn=sql.connect(root.filedb())
    c=conn.cursor()
    ### First time setup server:
    c.execute('''CREATE TABLE user (user_id varchar[50], user_password varchar[50], user_name varchar[50], user_affiliation varchar[50])''')
    c.execute('''CREATE TABLE files (project_id varchar[50], file varchar[50], status varchar[20])''')
    c.execute('''CREATE TABLE user_projects (user_id varchar[50], project_id varchar[50])''')
    c.execute('''CREATE TABLE project (project_id NUM PRIMARY_KEY UNIQUE NOT NULL, project_name varchar[50], project_short_description varchar[500], project_description varchar[2000], project_path varchar[500])''')
    c.execute('''CREATE TABLE project_status (user_id varchar[50], project_id varchar[50], sample_id varchar[50], status varchar[50])''')
    #c.execute('''CREATE TABLE metagenome (metagenome_id NUM PRIMARY_KEY UNIQUE NOT NULL, project_id NUM , metagenome_name varchar[50], metagenome_description varchar[50], fastq1 varchar[50], fastq2 varchar[50], location varchar[50], material varchar[50], country varchar[50], biome varchar[50], feature varchar[50], sequencing_method varchar[50])''')
    c.execute('''CREATE TABLE samples (sample_id NUM PRIMARY_KEY UNIQUE NOT NULL, project_id NUM , sample_name varchar[50], sample_set varchar[50], environment varchar[50], library_preparation varchar[50], reads1 varchar[50], reads2 varchar[50])''')
    c.execute('''CREATE TABLE version (version_id NUM PRIMARY_KEY UNIQUE NOT NULL, metagenome_id NUM, aligner_id NUM, aligner_parameters varchar[500], assembler_id NUM, assembler_parameters varchar[500], reference_id NUM)''')
    c.execute('''CREATE TABLE reference (reference_id integer PRIMARY_KEY unique not null, reference_name varchar[50], sequence_type varchar[50], reference_description varchar[2000], reference_path varchar[50], user_id varchar[50], seqfile varchar[200], taxofile varchar[200], functfile varchar[200])''')
    c.execute('''CREATE TABLE aligner (aligner_id NUM PRIMARY_KEY UNIQUE NOT NULL, aligner_name varchar[50] unique not null, aligner_default varchar[50], aligner_fast varchar[50], aligner_sensitive varchar [100])''')
    c.execute('''CREATE TABLE assembler (assembler_id NUM PRIMARY_KEY UNIQUE NOT NULL, assembler_name varchar[50] UNIQUE NOT NULL, assembler_default varchar[50], assembler_fast varchar[50], assembler_sensitive varchar[50])''')
    # values=(1, 'diamond', '-e 0.001 --id 60 --top 100', '-e 1e-10 --id 90 --top 100', '--sensitive -id 60 -e 0.05')
    # values=(1, u'idba_ud', u' ', u'--min_contig 500 --max_mismatch 1 ', u'--min_contig 50 --max_mismatch 3 ')
    # values = ['ncbi_genomes','prot','database from NCBI 2014, 5187 fully sequenced bacterial genomes', 'admin']
    # values = ['nanocellulose','''study of the process of the nano cellulose degradation','nanocellulose degradation', main_path+"/PROJECTS/"]
    c.execute('''CREATE TABLE assembly (sample_id varchar[50] not null, user_id varchar[50], project_id varchar[50], datasets varchar[5000])''')
    c.execute('''CREATE TABLE matches (sample_id varchar[50] not null, user_id varchar[50], project_id varchar[50], datasets varchar[5000])''')


    c.execute('''CREATE TABLE sample_run (sample_id varchar[50] not null, process varchar[500])''')
    conn.commit()
    conn.close()



## to play with the db do this:
'''
import app.lib.create_project as c
import app.lib.common.rootvar as r
x=c.insert_new_project.SQL(r.__FILEDB__)



'''
