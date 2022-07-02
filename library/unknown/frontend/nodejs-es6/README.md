## Nodejs 支持 ES6

Nodejs 默认不支持 ES6 的大多数语法，比如 import/export 等，在运行时会报错：

```
SyntaxError: Unexpected token import
    at createScript (vm.js:80:10)
    at Object.runInThisContext (vm.js:139:10)
    at Module._compile (module.js:616:28)
    at Object.Module._extensions..js (module.js:663:10)
    at Module.load (module.js:565:32)
    at tryModuleLoad (module.js:505:12)
    at Function.Module._load (module.js:497:3)
    at Function.Module.runMain (module.js:693:10)
    at startup (bootstrap_node.js:188:16)
    at bootstrap_node.js:609:3
```

### import/export 替代写法

一种解决方法是使用 `import` 和 `export` 替代写法：`require` 和 `module.exports`。

```
import { foo } from './foo'
```

可以写成：

```
const foo = require('./foo-es5')
```

```
export function foo() {
}
```

可以写成：

```
module.exports = foo
```

### babel

另一种解决方法是使用 `babel` 将 ES6 语法转换为 ES5 语法。

在 `package.json` 的 devDependencies 中添加依赖：

```
  "devDependencies": {
    "babel-cli": "^6.26.0",
    "babel-preset-env": "^1.3.2"
  }
```

并添加一个脚本，用于启动 `babel-node`：

```
  "scripts": {
    "es6": "babel-node index-es6.js --presets env"
  }
```

然后运行 `npm run es6`。