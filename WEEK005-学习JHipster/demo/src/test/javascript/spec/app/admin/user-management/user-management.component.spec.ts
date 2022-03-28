import { shallowMount, createLocalVue, Wrapper } from '@vue/test-utils';
import axios from 'axios';
import sinon from 'sinon';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { ToastPlugin } from 'bootstrap-vue';

import * as config from '@/shared/config/config';
import UserManagement from '@/admin/user-management/user-management.vue';
import UserManagementClass from '@/admin/user-management/user-management.component';
import UserManagementService from '@/admin/user-management/user-management.service';
import AlertService from '@/shared/alert/alert.service';

const localVue = createLocalVue();

localVue.use(ToastPlugin);
config.initVueApp(localVue);
const i18n = config.initI18N(localVue);
const store = config.initVueXStore(localVue);
localVue.component('font-awesome-icon', FontAwesomeIcon);
localVue.component('router-link', {});
localVue.component('jhi-sort-indicator', {});
localVue.directive('b-modal', {});

const axiosStub = {
  delete: sinon.stub(axios, 'delete'),
  get: sinon.stub(axios, 'get'),
  put: sinon.stub(axios, 'put'),
};

describe('UserManagement Component', () => {
  let wrapper: Wrapper<UserManagementClass>;
  let userManagement: UserManagementClass;

  const account = {
    firstName: 'John',
    lastName: 'Doe',
    email: 'john.doe@jhipster.org',
  };

  beforeEach(() => {
    axiosStub.put.reset();
    axiosStub.get.reset();
    axiosStub.get.resolves({ headers: {} });

    store.commit('authenticated', account);
    wrapper = shallowMount<UserManagementClass>(UserManagement, {
      store,
      i18n,
      localVue,
      stubs: {
        bPagination: true,
        jhiItemCount: true,
        bModal: true,
      },
      provide: {
        userManagementService: () => new UserManagementService(),
        alertService: () => new AlertService(),
      },
    });
    userManagement = wrapper.vm;
  });

  describe('OnInit', () => {
    it('Should call load all on init', async () => {
      // WHEN
      userManagement.loadAll();
      await userManagement.$nextTick();

      // THEN
      expect(axiosStub.get.calledWith(`api/admin/users?sort=id,asc&page=0&size=20`)).toBeTruthy();
    });
  });

  describe('setActive', () => {
    it('Should update user and call load all', async () => {
      // GIVEN
      axiosStub.put.resolves({});

      // WHEN
      userManagement.setActive({ id: 123 }, true);
      await userManagement.$nextTick();

      // THEN
      expect(axiosStub.put.calledWith(`api/admin/users`, { id: 123, activated: true })).toBeTruthy();
      expect(axiosStub.get.calledWith(`api/admin/users?sort=id,asc&page=0&size=20`)).toBeTruthy();
    });
  });

  describe('confirmDelete', () => {
    it('Should call delete service on confirmDelete', async () => {
      // GIVEN
      axiosStub.delete.resolves({
        headers: {
          'x-demoapp-alert': '',
          'x-demoapp-params': '',
        },
      });

      // WHEN
      userManagement.prepareRemove({ login: 123 });
      userManagement.deleteUser();
      await userManagement.$nextTick();

      // THEN
      expect(axiosStub.delete.calledWith('api/admin/users/' + 123)).toBeTruthy();
      expect(axiosStub.get.calledWith(`api/admin/users?sort=id,asc&page=0&size=20`)).toBeTruthy();
    });
  });

  describe('change order', () => {
    it('should change order and invert reverse', () => {
      // WHEN
      userManagement.changeOrder('dummy-order');

      // THEN
      expect(userManagement.propOrder).toEqual('dummy-order');
      expect(userManagement.reverse).toBe(true);
    });
  });
});
