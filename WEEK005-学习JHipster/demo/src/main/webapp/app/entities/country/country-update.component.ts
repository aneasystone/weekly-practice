import { Component, Vue, Inject } from 'vue-property-decorator';

import AlertService from '@/shared/alert/alert.service';

import RegionService from '@/entities/region/region.service';
import { IRegion } from '@/shared/model/region.model';

import { ICountry, Country } from '@/shared/model/country.model';
import CountryService from './country.service';

const validations: any = {
  country: {
    countryName: {},
  },
};

@Component({
  validations,
})
export default class CountryUpdate extends Vue {
  @Inject('countryService') private countryService: () => CountryService;
  @Inject('alertService') private alertService: () => AlertService;

  public country: ICountry = new Country();

  @Inject('regionService') private regionService: () => RegionService;

  public regions: IRegion[] = [];
  public isSaving = false;
  public currentLanguage = '';

  beforeRouteEnter(to, from, next) {
    next(vm => {
      if (to.params.countryId) {
        vm.retrieveCountry(to.params.countryId);
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
    if (this.country.id) {
      this.countryService()
        .update(this.country)
        .then(param => {
          this.isSaving = false;
          this.$router.go(-1);
          const message = this.$t('demoApp.country.updated', { param: param.id });
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
      this.countryService()
        .create(this.country)
        .then(param => {
          this.isSaving = false;
          this.$router.go(-1);
          const message = this.$t('demoApp.country.created', { param: param.id });
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

  public retrieveCountry(countryId): void {
    this.countryService()
      .find(countryId)
      .then(res => {
        this.country = res;
      })
      .catch(error => {
        this.alertService().showHttpError(this, error.response);
      });
  }

  public previousState(): void {
    this.$router.go(-1);
  }

  public initRelationships(): void {
    this.regionService()
      .retrieve()
      .then(res => {
        this.regions = res.data;
      });
  }
}
