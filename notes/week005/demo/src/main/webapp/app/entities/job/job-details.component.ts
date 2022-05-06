import { Component, Vue, Inject } from 'vue-property-decorator';

import { IJob } from '@/shared/model/job.model';
import JobService from './job.service';
import AlertService from '@/shared/alert/alert.service';

@Component
export default class JobDetails extends Vue {
  @Inject('jobService') private jobService: () => JobService;
  @Inject('alertService') private alertService: () => AlertService;

  public job: IJob = {};

  beforeRouteEnter(to, from, next) {
    next(vm => {
      if (to.params.jobId) {
        vm.retrieveJob(to.params.jobId);
      }
    });
  }

  public retrieveJob(jobId) {
    this.jobService()
      .find(jobId)
      .then(res => {
        this.job = res;
      })
      .catch(error => {
        this.alertService().showHttpError(this, error.response);
      });
  }

  public previousState() {
    this.$router.go(-1);
  }
}
