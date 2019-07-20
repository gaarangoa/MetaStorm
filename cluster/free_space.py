# This script will remove all the data that was incomplete
# when running MetaStorm, It is very useful for getting some
# extra space


from subprocess import Popen, PIPE
import os

p = Popen(['showq', '-u', 'gustavo1'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
output, err = p.communicate()

running_jobs = []
for line in output.split('\n'):
    line = line.split()
    try:
        running_jobs.append(int(line[0]))
    except:
        pass

job_paths = {}
for job_id in running_jobs:
    p = Popen(['checkjob', '-v', '{}'.format(job_id)],
              stdin=PIPE, stdout=PIPE, stderr=PIPE)
    output, err = p.communicate()
    job_path = ''
    for line in output.split('\n'):
        if "OutputFile" in line:
            job_path = line.split(':')[2]
    #
    if job_path:
        if 'MetaStorm' in job_path:
            fields = job_path.split('/')
            #
            sid = fields[-2]
            pid = fields[-4]
            pip = 'matches'
            if 'idba_ud' in job_path:
                pid = fields[-5]
                pip = 'assembly'
            #
            job_paths.update({'{}:{}'.format(pid, sid): {
                "sid": sid,
                "pip": pip,
                'pid': pid
            }})

# Get all project running jobs
p = Popen(['ls', '/groups/metastorm_cscee/MetaStorm/Files/PROJECTS/'],
          stdin=PIPE, stdout=PIPE, stderr=PIPE)
output, err = p.communicate()


def remove_files(pid, sid, pip):
    if not sid:
        return 0
    remove = '*.matches *.daa *.sam'
    if pip == 'assembly':
        pip = 'assembly/idba_ud'
        remove = '*.matches *.daa *.sam align-* graph-* kmer local-contig-*'
    #
    path = '/groups/metastorm_cscee/MetaStorm/Files/PROJECTS/{}/{}/{}'.format(
        pid, pip, sid)
    #
    try:
        print(path)
        os.system('cd {} && rm {}'.format(path, remove))
    except Exception as inst:
        print(inst)


# remove files that are in the assembly and matches pipeline
for pid in output.split('\n'):
    sample_path = '/groups/metastorm_cscee/MetaStorm/Files/PROJECTS/{}/assembly/idba_ud/'.format(
        pid)
    p = Popen(['ls', sample_path], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    sample_base_string, err = p.communicate()
    #
    samples = sample_base_string.split('\n')
    #
    for sample in samples:
        # print('processing: sid:{}, pid:{}'.format(sample, pid))
        try:
            print('still running: ', job_paths["{}:{}".format(pid, sample)])
        except:
            status = remove_files(pid, sample, 'matches')
            status = remove_files(pid, sample, 'assembly')
