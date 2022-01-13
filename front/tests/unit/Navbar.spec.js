import { mount, createLocalVue } from '@vue/test-utils';
import Navbar from '@/components/shared/Navbar';
import Vuetify from 'vuetify';

describe('Navbar.vue', () => {
  let vuetify;
  const localVue = createLocalVue();
  beforeEach(() => {
    vuetify = new Vuetify();
  });

  it('Is a Vue instance', () => {
    const wrapper = mount(Navbar, {
      localVue,
      vuetify
    });
    expect(wrapper.isVueInstance).toBeTruthy();
    wrapper.destroy();
  });

  it('Check if user initially sees accounts button', () => {
    const wrapper = mount(Navbar, {
      localVue,
      vuetify
    });
    expect(wrapper.find('[data-test="accounts"]').exists()).toBeFalsy();
  });

  it('Check if user initially sees logout button', () => {
    const wrapper = mount(Navbar, {
      localVue,
      vuetify
    });
    expect(wrapper.find('[data-test="logout"]').exists()).toBeFalsy();
  });

  it('Check if logged in (normal) user sees accounts button', async () => {
    const wrapper = mount(Navbar, {
      localVue,
      vuetify
    });
    await wrapper.setData({ loggedIn: true });
    expect(wrapper.find('[data-test="accounts"]').exists()).toBeFalsy();
  });

  it('Check if logged in (admin) user sees accounts button', async () => {
    const wrapper = mount(Navbar, {
      localVue,
      vuetify
    });
    await wrapper.setData({ loggedIn: true });
    await wrapper.setData({ adminLoggedIn: true });
    expect(wrapper.find('[data-test="accounts"]').exists()).toBeTruthy();
  });

  it('Check if logged in user sees logout button', async () => {
    const wrapper = mount(Navbar, {
      localVue,
      vuetify
    });
    await wrapper.setData({ loggedIn: true });
    expect(wrapper.find('[data-test="logout"]').exists()).toBeTruthy();
  });
});
