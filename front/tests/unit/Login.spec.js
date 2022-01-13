import { mount, createLocalVue } from '@vue/test-utils';
import Login from '@/Auth/Login';
import Vuetify from 'vuetify';

describe('Login.vue', () => {
  let vuetify;
  const localVue = createLocalVue();
  let wrapper;
  beforeEach(() => {
    const div = document.createElement('div');
    div.id = 'root';
    document.body.appendChild(div);
    vuetify = new Vuetify();
    wrapper = mount(Login, {
      localVue,
      vuetify,
      attachTo: '#root'
    });
  });

  afterEach(() => {
    wrapper.destroy();
  });

  it('Is a Vue instance', () => {
    expect(wrapper.isVueInstance).toBeTruthy();
  });

  it('Checks if user initially sees loginBox', () => {
    const wrapper = mount(Login, {
      localVue,
      vuetify
    });
    expect(wrapper.find('.loginBox').exists()).toBe(false);
    wrapper.destroy();
  });

  it('Checks if user without cookies sees username field', async () => {
    await wrapper.setData({ loginBox: true });
    await wrapper.setData({ loggedKey: 1 });

    expect(wrapper.find('[data-test="username"]').exists()).toBe(true);
  });

  it('Checks if user without cookies sees password field', async () => {
    await wrapper.setData({ loginBox: true });
    await wrapper.setData({ loggedKey: 1 });

    expect(wrapper.find('[data-test="password"]').exists()).toBe(true);
  });

  it('Checks if user see required validation for blank username field', async () => {
    await wrapper.setData({ loginBox: true });
    await wrapper.setData({ loggedKey: 1 });
    await wrapper.find('[data-test="username"]').trigger('focus');
    await wrapper.find('[data-test="password"]').trigger('focus');

    expect(wrapper.find('.username .v-text-field__details').text()).toContain('Required.');
  });

  it('Checks if user see required validation for blank password field', async () => {
    await wrapper.setData({ loginBox: true });
    await wrapper.setData({ loggedKey: 1 });
    await wrapper.find('[data-test="password"]').trigger('focus');
    await wrapper.find('[data-test="username"]').trigger('focus');

    expect(wrapper.find('.password .v-text-field__details').text()).toContain('Required.');
  });

  it('Checks if user see required validation for filled username field', async () => {
    await wrapper.setData({ loginBox: true });
    await wrapper.setData({ loggedKey: 1 });
    await wrapper.find('[data-test="username"]').trigger('focus');
    await wrapper.setData({ email: 'test' });
    await wrapper.find('[data-test="password"]').trigger('focus');

    expect(wrapper.find('.username .v-text-field__details').text()).toContain('');
  });

  it('Checks if user see required validation for filled password field', async () => {
    await wrapper.setData({ loginBox: true });
    await wrapper.setData({ loggedKey: 1 });
    await wrapper.find('[data-test="password"]').trigger('focus');
    await wrapper.setData({ password: 'test' });
    await wrapper.find('[data-test="username"]').trigger('focus');

    expect(wrapper.find('.password .v-text-field__details').text()).toContain('');
  });
});
