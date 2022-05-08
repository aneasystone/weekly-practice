/* tslint:disable max-line-length */
import { shallowMount, createLocalVue, Wrapper } from '@vue/test-utils';
import sinon, { SinonStubbedInstance } from 'sinon';
import VueRouter from 'vue-router';

import * as config from '@/shared/config/config';
import EmployeeDetailComponent from '@/entities/employee/employee-details.vue';
import EmployeeClass from '@/entities/employee/employee-details.component';
import EmployeeService from '@/entities/employee/employee.service';
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
  describe('Employee Management Detail Component', () => {
    let wrapper: Wrapper<EmployeeClass>;
    let comp: EmployeeClass;
    let employeeServiceStub: SinonStubbedInstance<EmployeeService>;

    beforeEach(() => {
      employeeServiceStub = sinon.createStubInstance<EmployeeService>(EmployeeService);

      wrapper = shallowMount<EmployeeClass>(EmployeeDetailComponent, {
        store,
        i18n,
        localVue,
        router,
        provide: { employeeService: () => employeeServiceStub, alertService: () => new AlertService() },
      });
      comp = wrapper.vm;
    });

    describe('OnInit', () => {
      it('Should call load all on init', async () => {
        // GIVEN
        const foundEmployee = { id: 123 };
        employeeServiceStub.find.resolves(foundEmployee);

        // WHEN
        comp.retrieveEmployee(123);
        await comp.$nextTick();

        // THEN
        expect(comp.employee).toBe(foundEmployee);
      });
    });

    describe('Before route enter', () => {
      it('Should retrieve data', async () => {
        // GIVEN
        const foundEmployee = { id: 123 };
        employeeServiceStub.find.resolves(foundEmployee);

        // WHEN
        comp.beforeRouteEnter({ params: { employeeId: 123 } }, null, cb => cb(comp));
        await comp.$nextTick();

        // THEN
        expect(comp.employee).toBe(foundEmployee);
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
