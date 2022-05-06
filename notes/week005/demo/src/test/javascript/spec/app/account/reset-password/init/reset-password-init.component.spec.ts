import { createLocalVue, shallowMount, Wrapper } from '@vue/test-utils';
import axios from 'axios';
import sinon from 'sinon';
import * as config from '@/shared/config/config';
import ResetPasswordInit from '@/account/reset-password/init/reset-password-init.vue';
import ResetPasswordInitClass from '@/account/reset-password/init/reset-password-init.component';

const localVue = createLocalVue();

config.initVueApp(localVue);
const i18n = config.initI18N(localVue);

const axiosStub = {
  get: sinon.stub(axios, 'get'),
  post: sinon.stub(axios, 'post'),
};

describe('Reset Component Init', () => {
  let wrapper: Wrapper<ResetPasswordInitClass>;
  let resetPasswordInit: ResetPasswordInitClass;

  beforeEach(() => {
    axiosStub.post.reset();
    wrapper = shallowMount<ResetPasswordInitClass>(ResetPasswordInit, {
      i18n,
      localVue,
    });
    resetPasswordInit = wrapper.vm;
  });

  it('should reset request be a success', async () => {
    // Given
    axiosStub.post.resolves();

    // When
    await resetPasswordInit.requestReset();

    // Then
    expect(resetPasswordInit.success).toBeTruthy();
  });

  it('should reset request fail as an error', async () => {
    // Given
    axiosStub.post.rejects({
      response: {
        status: null,
        data: {
          type: null,
        },
      },
    });

    // When
    resetPasswordInit.requestReset();
    await resetPasswordInit.$nextTick();

    // Then
    expect(resetPasswordInit.success).toBeNull();
    expect(resetPasswordInit.error).toEqual('ERROR');
  });
});
