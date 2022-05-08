import { Component, Vue, Inject } from 'vue-property-decorator';

import AlertService from '@/shared/alert/alert.service';

import { IFoo, Foo } from '@/shared/model/foo.model';
import FooService from './foo.service';

const validations: any = {
  foo: {
    name: {},
  },
};

@Component({
  validations,
})
export default class FooUpdate extends Vue {
  @Inject('fooService') private fooService: () => FooService;
  @Inject('alertService') private alertService: () => AlertService;

  public foo: IFoo = new Foo();
  public isSaving = false;
  public currentLanguage = '';

  beforeRouteEnter(to, from, next) {
    next(vm => {
      if (to.params.fooId) {
        vm.retrieveFoo(to.params.fooId);
      }
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
    if (this.foo.id) {
      this.fooService()
        .update(this.foo)
        .then(param => {
          this.isSaving = false;
          this.$router.go(-1);
          const message = this.$t('demoApp.foo.updated', { param: param.id });
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
      this.fooService()
        .create(this.foo)
        .then(param => {
          this.isSaving = false;
          this.$router.go(-1);
          const message = this.$t('demoApp.foo.created', { param: param.id });
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

  public retrieveFoo(fooId): void {
    this.fooService()
      .find(fooId)
      .then(res => {
        this.foo = res;
      })
      .catch(error => {
        this.alertService().showHttpError(this, error.response);
      });
  }

  public previousState(): void {
    this.$router.go(-1);
  }

  public initRelationships(): void {}
}
