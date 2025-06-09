// vue-shims.d.ts 或者 vite-env.d.ts 中定义
declare module '*.vue' {
  import { DefineComponent } from 'vue';
  const component: DefineComponent<{}, {}, any>;
  export default component;
}
