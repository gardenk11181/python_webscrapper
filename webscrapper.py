from indeed import get_jobs as get_indeed_jobs
from stackoverflow import get_jobs as get_so_jobs
from save import save_to_file

def save_jobs_csv():
    indeed_jobs = get_indeed_jobs()
    so_jobs = get_so_jobs()
    jobs = indeed_jobs + so_jobs
    save_to_file(jobs)

# save_jobs_csv()

