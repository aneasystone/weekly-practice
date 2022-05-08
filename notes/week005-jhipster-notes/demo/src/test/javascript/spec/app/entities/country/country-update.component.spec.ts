/* tslint:disable max-line-length */
import { shallowMount, createLocalVue, Wrapper } from '@vue/test-utils';
import sinon, { SinonStubbedInstance } from 'sinon';
import Router from 'vue-router';
import { ToastPlugin } from 'bootstrap-vue';

import * as config from '@/shared/config/config';
import CountryUpdateComponent from '@/entities/country/country-update.vue';
import CountryClass from '@/entities/country/country-update.component';
import CountryService from '@/entities/country/country.service';

import RegionService from '@/entities/region/region.service';
import AlertService from '@/shared/alert/alert.service';

const localVue = createLocalVue();

config.initVueApp(localVue);
const i18n = config.initI18N(localVue);
const store = config.initVueXStore(localVue);
const router = new Router();
localVue.use(Router);
localVue.use(ToastPlugin);
localVue.component('font-awesome-icon', {});
localVue.component('b-input-group', {});
localVue.component('b-input-group-prepend', {});
localVue.component('b-form-datepicker', {});
localVue.component('b-form-input', {});

describe('Component Tests', () => {
  describe('Country Management Update Component', () => {
    let wrapper: Wrapper<CountryClass>;
    let comp: CountryClass;
    let countryServiceStub: SinonStubbedInstance<CountryService>;

    beforeEach(() => {
      countryServiceStub = sinon.createStubInstance<CountryService>(CountryService);

      wrapper = shallowMount<CountryClass>(CountryUpdateComponent, {
        store,
        i18n,
        localVue,
        router,
        provide: {
          countryService: () => countryServiceStub,
          alertService: () => new AlertService(),

          regionService: () =>
            sinon.createStubInstance<RegionService>(RegionService, {
              retrieve: sinon.stub().resolves({}),
            } as any),
        },
      });
      comp = wrapper.vm;
    });

    describe('save', () => {
      it('Should call update service on save for existing entity', async () => {
        // GIVEN
        const entity = { id: 123 };
        comp.country = entity;
        countryServiceStub.update.resolves(entity);

        // WHEN
        comp.save();
        await comp.$nextTick();

        // THEN
        expect(countryServiceStub.update.calledWith(entity)).toBeTruthy();
        expect(comp.isSaving).toEqual(false);
      });

      it('Should call create service on save for new entity', async () => {
        // GIVEN
        const entity = {};
        comp.country = entity;
        countryServiceStub.create.resolves(entity);

        // WHEN
        comp.save();
        await comp.$nextTick();

        // THEN
        expect(countryServiceStub.create.calledWith(entity)).toBeTruthy();
        expect(comp.isSaving).toEqual(false);
      });
    });

    describe('Before route enter', () => {
      it('Should retrieve data', async () => {
        // GIVEN
        const foundCountry = { id: 123 };
        countryServiceStub.find.resolves(foundCountry);
        countryServiceStub.retrieve.resolves([foundCountry]);

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
