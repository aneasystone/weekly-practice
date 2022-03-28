import sinon from 'sinon';

import AlertService from '@/shared/alert/alert.service';
import Vue from 'vue';
import { createLocalVue, mount, shallowMount } from '@vue/test-utils';
const translationStub = sinon.stub();
const toastStub = sinon.stub();

const vueInstance = {
  $t: translationStub,
  $root: {
    $bvToast: {
      toast: toastStub,
    },
  },
};

describe('Alert Service test suite', () => {
  let alertService: AlertService;

  beforeEach(() => {
    translationStub.reset();
    toastStub.reset();
    alertService = new AlertService();
  });

  it('should show error toast with translation/message', async () => {
    const message = 'translatedMessage';
    const translationKey = 'err.code';

    // GIVEN
    translationStub.withArgs(translationKey).returns(message);

    // WHEN
    alertService.showError((<any>vueInstance) as Vue, translationKey);

    //THEN
    expect(translationStub.withArgs(translationKey).callCount).toEqual(1);
    expect(
      toastStub.calledOnceWith(message, {
        toaster: 'b-toaster-top-center',
        title: 'Error',
        variant: 'danger',
        solid: true,
        autoHideDelay: 5000,
      })
    ).toBeTruthy();
  });

  it('should show not reachable toast when http status = 0', async () => {
    const translationKey = 'error.server.not.reachable';
    const message = 'Server not reachable';
    const httpErrorResponse = {
      status: 0,
    };
    // GIVEN
    translationStub.withArgs(translationKey).returns(message);

    // WHEN
    alertService.showHttpError((<any>vueInstance) as Vue, httpErrorResponse);

    //THEN
    expect(translationStub.withArgs(translationKey).callCount).toEqual(1);
    expect(
      toastStub.calledOnceWith(message, {
        toaster: 'b-toaster-top-center',
        title: 'Error',
        variant: 'danger',
        solid: true,
        autoHideDelay: 5000,
      })
    ).toBeTruthy();
  });

  it('should show parameterized error toast when http status = 400 and entity headers', async () => {
    const translationKey = 'error.update';
    const message = 'Updation Error';
    const httpErrorResponse = {
      status: 400,
      headers: {
        'x-jhipsterapp-error': translationKey,
        'x-jhipsterapp-params': 'dummyEntity',
      },
    };
    // GIVEN
    translationStub.withArgs(translationKey).returns(message);
    translationStub.withArgs('global.menu.entities.dummyEntity').returns('DummyEntity');

    // WHEN
    alertService.showHttpError((<any>vueInstance) as Vue, httpErrorResponse);

    //THEN
    expect(translationStub.withArgs(translationKey, { entityName: 'DummyEntity' }).callCount).toEqual(1);
    expect(
      toastStub.calledOnceWith(message, {
        toaster: 'b-toaster-top-center',
        title: 'Error',
        variant: 'danger',
        solid: true,
        autoHideDelay: 5000,
      })
    ).toBeTruthy();
  });
});
