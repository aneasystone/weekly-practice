/* tslint:disable max-line-length */
import { shallowMount, createLocalVue, Wrapper } from '@vue/test-utils';
import sinon, { SinonStubbedInstance } from 'sinon';
import VueRouter from 'vue-router';

import * as config from '@/shared/config/config';
import FooDetailComponent from '@/entities/foo/foo-details.vue';
import FooClass from '@/entities/foo/foo-details.component';
import FooService from '@/entities/foo/foo.service';
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
  describe('Foo Management Detail Component', () => {
    let wrapper: Wrapper<FooClass>;
    let comp: FooClass;
    let fooServiceStub: SinonStubbedInstance<FooService>;

    beforeEach(() => {
      fooServiceStub = sinon.createStubInstance<FooService>(FooService);

      wrapper = shallowMount<FooClass>(FooDetailComponent, {
        store,
        i18n,
        localVue,
        router,
        provide: { fooService: () => fooServiceStub, alertService: () => new AlertService() },
      });
      comp = wrapper.vm;
    });

    describe('OnInit', () => {
      it('Should call load all on init', async () => {
        // GIVEN
        const foundFoo = { id: 123 };
        fooServiceStub.find.resolves(foundFoo);

        // WHEN
        comp.retrieveFoo(123);
        await comp.$nextTick();

        // THEN
        expect(comp.foo).toBe(foundFoo);
      });
    });

    describe('Before route enter', () => {
      it('Should retrieve data', async () => {
        // GIVEN
        const foundFoo = { id: 123 };
        fooServiceStub.find.resolves(foundFoo);

        // WHEN
        comp.beforeRouteEnter({ params: { fooId: 123 } }, null, cb => cb(comp));
        await comp.$nextTick();

        // THEN
        expect(comp.foo).toBe(foundFoo);
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
