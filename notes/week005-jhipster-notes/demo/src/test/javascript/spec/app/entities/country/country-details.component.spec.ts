/* tslint:disable max-line-length */
import { shallowMount, createLocalVue, Wrapper } from '@vue/test-utils';
import sinon, { SinonStubbedInstance } from 'sinon';
import VueRouter from 'vue-router';

import * as config from '@/shared/config/config';
import CountryDetailComponent from '@/entities/country/country-details.vue';
import CountryClass from '@/entities/country/country-details.component';
import CountryService from '@/entities/country/country.service';
import router from '@/router';
import AlertService from '@/shared/alert/alert.service';

const localVue = createLocalVue();
localVue.use(VueRouter);

config.initVueApp(localVue);
const i18n = config.initI18N(localVue);
const store = config.initVueXStore(localVue);
localVue.component('font-awesome-icon', {});
localVue.component('router-link', {});

describe('Component Tests', () => {
  describe('Country Management Detail Component', () => {
    let wrapper: Wrapper<CountryClass>;
    let comp: CountryClass;
    let countryServiceStub: SinonStubbedInstance<CountryService>;

    beforeEach(() => {
      countryServiceStub = sinon.createStubInstance<CountryService>(CountryService);

      wrapper = shallowMount<CountryClass>(CountryDetailComponent, {
        store,
        i18n,
        localVue,
        router,
        provide: { countryService: () => countryServiceStub, alertService: () => new AlertService() },
      });
      comp = wrapper.vm;
    });

    describe('OnInit', () => {
      it('Should call load all on init', async () => {
        // GIVEN
        const foundCountry = { id: 123 };
        countryServiceStub.find.resolves(foundCountry);

        // WHEN
        comp.retrieveCountry(123);
        await comp.$nextTick();

        // THEN
        expect(comp.country).toBe(foundCountry);
      });
    });

    describe('Before route enter', () => {
      it('Should retrieve data', async () => {
        // GIVEN
        const foundCountry = { id: 123 };
        countryServiceStub.find.resolves(foundCountry);

        // WHEN
        comp.beforeRouteEnter({ params: { countryId: 123 } }, null, cb => cb(comp));
        await comp.$nextTick();

        // THEN
        expect(comp.country).toBe(foundCountry);
      });
    });

    describe('Previous state', () => {
      it('Should go previous state', async () => {
        comp.previousState();
        await comp.$nextTick();

        expect(comp.$router.currentRoute.fullPath).toContain('/');
      });
    });
  });
});
