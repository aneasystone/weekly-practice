/* tslint:disable max-line-length */
import { shallowMount, createLocalVue, Wrapper } from '@vue/test-utils';
import sinon, { SinonStubbedInstance } from 'sinon';
import Router from 'vue-router';
import { ToastPlugin } from 'bootstrap-vue';

import * as config from '@/shared/config/config';
import DepartmentUpdateComponent from '@/entities/department/department-update.vue';
import DepartmentClass from '@/entities/department/department-update.component';
import DepartmentService from '@/entities/department/department.service';

import LocationService from '@/entities/location/location.service';

import EmployeeService from '@/entities/employee/employee.service';
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
  describe('Department Management Update Component', () => {
    let wrapper: Wrapper<DepartmentClass>;
    let comp: DepartmentClass;
    let departmentServiceStub: SinonStubbedInstance<DepartmentService>;

    beforeEach(() => {
      departmentServiceStub = sinon.createStubInstance<DepartmentService>(DepartmentService);

      wrapper = shallowMount<DepartmentClass>(DepartmentUpdateComponent, {
        store,
        i18n,
        localVue,
        router,
        provide: {
          departmentService: () => departmentServiceStub,
          alertService: () => new AlertService(),

          locationService: () =>
            sinon.createStubInstance<LocationService>(LocationService, {
              retrieve: sinon.stub().resolves({}),
            } as any),

          employeeService: () =>
            sinon.createStubInstance<EmployeeService>(EmployeeService, {
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
        comp.department = entity;
        departmentServiceStub.update.resolves(entity);

        // WHEN
        comp.save();
        await comp.$nextTick();

        // THEN
        expect(departmentServiceStub.update.calledWith(entity)).toBeTruthy();
        expect(comp.isSaving).toEqual(false);
      });

      it('Should call create service on save for new entity', async () => {
        // GIVEN
        const entity = {};
        comp.department = entity;
        departmentServiceStub.create.resolves(entity);

        // WHEN
        comp.save();
        await comp.$nextTick();

        // THEN
        expect(departmentServiceStub.create.calledWith(entity)).toBeTruthy();
        expect(comp.isSaving).toEqual(false);
      });
    });

    describe('Before route enter', () => {
      it('Should retrieve data', async () => {
        // GIVEN
        const foundDepartment = { id: 123 };
        departmentServiceStub.find.resolves(foundDepartment);
        departmentServiceStub.retrieve.resolves([foundDepartment]);

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
