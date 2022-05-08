import { Component, Vue, Inject } from 'vue-property-decorator';

import { IJobHistory } from '@/shared/model/job-history.model';
import JobHistoryService from './job-history.service';
import AlertService from '@/shared/alert/alert.service';

@Component
export default class JobHistoryDetails extends Vue {
  @Inject('jobHistoryService') private jobHistoryService: () => JobHistoryService;
  @Inject('alertService') private alertService: () => AlertService;

  public jobHistory: IJobHistory = {};

  beforeRouteEnter(to, from, next) {
    next(vm => {
      if (to.params.jobHistoryId) {
        vm.retrieveJobHistory(to.params.jobHistoryId);
      }
    });
  }

  public retrieveJobHistory(jobHistoryId) {
    this.jobHistoryService()
      .find(jobHistoryId)
      .then(res => {
        this.jobHistory = res;
      })
      .catch(error => {
        this.alertService().showHttpError(this, error.response);
      });
  }

  public previousState() {
    this.$router.go(-1);
  }
}
