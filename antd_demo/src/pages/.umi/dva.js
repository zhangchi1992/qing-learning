import dva from 'dva';
import { Component } from 'react';
import createLoading from 'dva-loading';
import history from '@tmp/history';

let app = null;

export function _onCreate() {
  const plugins = require('umi/_runtimePlugin');
  const runtimeDva = plugins.mergeConfig('dva');
  app = dva({
    history,
    
    ...(runtimeDva.config || {}),
    ...(window.g_useSSR ? { initialState: window.g_initialData } : {}),
  });
  
  app.use(createLoading());
  (runtimeDva.plugins || []).forEach(plugin => {
    app.use(plugin);
  });
  
  app.model({ namespace: 'global', ...(require('/Users/xiangquan/Public/own_project/antd_demo/src/models/global.js').default) });
app.model({ namespace: 'login', ...(require('/Users/xiangquan/Public/own_project/antd_demo/src/models/login.js').default) });
app.model({ namespace: 'setting', ...(require('/Users/xiangquan/Public/own_project/antd_demo/src/models/setting.js').default) });
app.model({ namespace: 'user', ...(require('/Users/xiangquan/Public/own_project/antd_demo/src/models/user.js').default) });
app.model({ namespace: 'model', ...(require('/Users/xiangquan/Public/own_project/antd_demo/src/pages/user/register/model.js').default) });
app.model({ namespace: 'model', ...(require('/Users/xiangquan/Public/own_project/antd_demo/src/pages/home/model.jsx').default) });
app.model({ namespace: 'model', ...(require('/Users/xiangquan/Public/own_project/antd_demo/src/pages/videos/model.js').default) });
app.model({ namespace: 'model', ...(require('/Users/xiangquan/Public/own_project/antd_demo/src/pages/articles/model.js').default) });
app.model({ namespace: 'model', ...(require('/Users/xiangquan/Public/own_project/antd_demo/src/pages/bi/model.jsx').default) });
  return app;
}

export function getApp() {
  return app;
}

export class _DvaContainer extends Component {
  render() {
    const app = getApp();
    app.router(() => this.props.children);
    return app.start()();
  }
}
