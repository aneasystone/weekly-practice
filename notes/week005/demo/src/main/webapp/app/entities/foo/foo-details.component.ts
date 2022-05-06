import { Component, Vue, Inject } from 'vue-property-decorator';

import { IFoo } from '@/shared/model/foo.model';
import FooService from './foo.service';
import AlertService from '@/shared/alert/alert.service';

@Component
export default class FooDetails extends Vue {
  @Inject('fooService') private fooService: () => FooService;
  @Inject('alertService') private alertService: () => AlertService;

  public foo: IFoo = {};

  beforeRouteEnter(to, from, next) {
    next(vm => {
      if (to.params.fooId) {
        vm.retrieveFoo(to.params.fooId);
      }
    });
  }

  public retrieveFoo(fooId) {
    this.fooService()
      .find(fooId)
      .then(res => {
        this.foo = res;
      })
      .catch(error => {
        this.alertService().showHttpError(this, error.response);
      });
  }

  public previousState() {
    this.$router.go(-1);
  }
}
