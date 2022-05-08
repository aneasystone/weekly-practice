import { Component, Vue, Inject } from 'vue-property-decorator';

import { IDepartment } from '@/shared/model/department.model';
import DepartmentService from './department.service';
import AlertService from '@/shared/alert/alert.service';

@Component
export default class DepartmentDetails extends Vue {
  @Inject('departmentService') private departmentService: () => DepartmentService;
  @Inject('alertService') private alertService: () => AlertService;

  public department: IDepartment = {};

  beforeRouteEnter(to, from, next) {
    next(vm => {
      if (to.params.departmentId) {
        vm.retrieveDepartment(to.params.departmentId);
      }
    });
  }

  public retrieveDepartment(departmentId) {
    this.departmentService()
      .find(departmentId)
      .then(res => {
        this.department = res;
      })
      .catch(error => {
        this.alertService().showHttpError(this, error.response);
      });
  }

  public previousState() {
    this.$router.go(-1);
  }
}
