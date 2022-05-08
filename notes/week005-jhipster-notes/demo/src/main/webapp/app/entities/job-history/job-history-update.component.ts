import { Component, Vue, Inject } from 'vue-property-decorator';

import dayjs from 'dayjs';
import { DATE_TIME_LONG_FORMAT } from '@/shared/date/filters';

import AlertService from '@/shared/alert/alert.service';

import JobService from '@/entities/job/job.service';
import { IJob } from '@/shared/model/job.model';

import DepartmentService from '@/entities/department/department.service';
import { IDepartment } from '@/shared/model/department.model';

import EmployeeService from '@/entities/employee/employee.service';
import { IEmployee } from '@/shared/model/employee.model';

import { IJobHistory, JobHistory } from '@/shared/model/job-history.model';
import JobHistoryService from './job-history.service';
import { Language } from '@/shared/model/enumerations/language.model';

const validations: any = {
  jobHistory: {
    startDate: {},
    endDate: {},
    language: {},
  },
};

@Component({
  validations,
})
export default class JobHistoryUpdate extends Vue {
  @Inject('jobHistoryService') private jobHistoryService: () => JobHistoryService;
  @Inject('alertService') private alertService: () => AlertService;

  public jobHistory: IJobHistory = new JobHistory();

  @Inject('jobService') private jobService: () => JobService;

  public jobs: IJob[] = [];

  @Inject('departmentService') private departmentService: () => DepartmentService;

  public departments: IDepartment[] = [];

  @Inject('employeeService') private employeeService: () => EmployeeService;

  public employees: IEmployee[] = [];
  public languageValues: string[] = Object.keys(Language);
  public isSaving = false;
  public currentLanguage = '';

  beforeRouteEnter(to, from, next) {
    next(vm => {
      if (to.params.jobHistoryId) {
        vm.retrieveJobHistory(to.params.jobHistoryId);
      }
      vm.initRelationships();
    });
  }

  created(): void {
    this.currentLanguage = this.$store.getters.currentLanguage;
    this.$store.watch(
      () => this.$store.getters.currentLanguage,
      () => {
        this.currentLanguage = this.$store.getters.currentLanguage;
      }
    );
  }

  public save(): void {
    this.isSaving = true;
    if (this.jobHistory.id) {
      this.jobHistoryService()
        .update(this.jobHistory)
        .then(param => {
          this.isSaving = false;
          this.$router.go(-1);
          const message = this.$t('demoApp.jobHistory.updated', { param: param.id });
          return this.$root.$bvToast.toast(message.toString(), {
            toaster: 'b-toaster-top-center',
            title: 'Info',
            variant: 'info',
            solid: true,
            autoHideDelay: 5000,
          });
        })
        .catch(error => {
          this.isSaving = false;
          this.alertService().showHttpError(this, error.response);
        });
    } else {
      this.jobHistoryService()
        .create(this.jobHistory)
        .then(param => {
          this.isSaving = false;
          this.$router.go(-1);
          const message = this.$t('demoApp.jobHistory.created', { param: param.id });
          this.$root.$bvToast.toast(message.toString(), {
            toaster: 'b-toaster-top-center',
            title: 'Success',
            variant: 'success',
            solid: true,
            autoHideDelay: 5000,
          });
        })
        .catch(error => {
          this.isSaving = false;
          this.alertService().showHttpError(this, error.response);
        });
    }
  }

  public convertDateTimeFromServer(date: Date): string {
    if (date && dayjs(date).isValid()) {
      return dayjs(date).format(DATE_TIME_LONG_FORMAT);
    }
    return null;
  }

  public updateInstantField(field, event) {
    if (event.target.value) {
      this.jobHistory[field] = dayjs(event.target.value, DATE_TIME_LONG_FORMAT);
    } else {
      this.jobHistory[field] = null;
    }
  }

  public updateZonedDateTimeField(field, event) {
    if (event.target.value) {
      this.jobHistory[field] = dayjs(event.target.value, DATE_TIME_LONG_FORMAT);
    } else {
      this.jobHistory[field] = null;
    }
  }

  public retrieveJobHistory(jobHistoryId): void {
    this.jobHistoryService()
      .find(jobHistoryId)
      .then(res => {
        res.startDate = new Date(res.startDate);
        res.endDate = new Date(res.endDate);
        this.jobHistory = res;
      })
      .catch(error => {
        this.alertService().showHttpError(this, error.response);
      });
  }

  public previousState(): void {
    this.$router.go(-1);
  }

  public initRelationships(): void {
    this.jobService()
      .retrieve()
      .then(res => {
        this.jobs = res.data;
      });
    this.departmentService()
      .retrieve()
      .then(res => {
        this.departments = res.data;
      });
    this.employeeService()
      .retrieve()
      .then(res => {
        this.employees = res.data;
      });
  }
}
