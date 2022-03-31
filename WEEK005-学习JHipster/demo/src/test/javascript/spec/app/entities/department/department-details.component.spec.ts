/* tslint:disable max-line-length */
import { shallowMount, createLocalVue, Wrapper } from '@vue/test-utils';
import sinon, { SinonStubbedInstance } from 'sinon';
import VueRouter from 'vue-router';

import * as config from '@/shared/config/config';
import DepartmentDetailComponent from '@/entities/department/department-details.vue';
import DepartmentClass from '@/entities/department/department-details.component';
import DepartmentService from '@/entities/department/department.service';
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
  describe('Department Management Detail Component', () => {
    let wrapper: Wrapper<DepartmentClass>;
    let comp: DepartmentClass;
    let departmentServiceStub: SinonStubbedInstance<DepartmentService>;

    beforeEach(() => {
      departmentServiceStub = sinon.createStubInstance<DepartmentService>(DepartmentService);

      wrapper = shallowMount<DepartmentClass>(DepartmentDetailComponent, {
        store,
        i18n,
        localVue,
        router,
        provide: { departmentService: () => departmentServiceStub, alertService: () => new AlertService() },
      });
      comp = wrapper.vm;
    });

    describe('OnInit', () => {
      it('Should call load all on init', async () => {
        // GIVEN
        const foundDepartment = { id: 123 };
        departmentServiceStub.find.resolves(foundDepartment);

        // WHEN
        comp.retrieveDepartment(123);
        await comp.$nextTick();

        // THEN
        expect(comp.department).toBe(foundDepartment);
      });
    });

    describe('Before route enter', () => {
      it('Should retrieve data', async () => {
        // GIVEN
        const foundDepartment = { id: 123 };
        departmentServiceStub.find.resolves(foundDepartment);

        // WHEN
        comp.beforeRouteEnter({ params: { departmentId: 123 } }, null, cb => cb(comp));
        await comp.$nextTick();

        // THEN
        expect(comp.department).toBe(foundDepartment);
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
