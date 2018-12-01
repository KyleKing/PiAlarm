module.exports = {
  "env": {
    "browser": true,
    "es6": true
  },
  "extends": [
    "eslint:recommended",
    "plugin:security/recommended",
    "fbjs"
  ],
  "parserOptions": {
    "ecmaFeatures": {
      "jsx": true
    },
    "ecmaVersion": 7,
    "sourceType": "module"
  },
  "plugins": [
    "optimize-regex",
    "react",
    "security",
    "no-loops",
    "array-func"
  ],
  "rules": {
    "camelcase": 2,
    "class-methods-use-this": 0,
    "comma-dangle": [
      "error",
      "always-multiline"
    ],
    "comma-spacing": [
      "error",
      {
        "after": true,
        "before": false
      }
    ],
    "comments": 65,
    "constructor-super": 2,
    "curly": [
      "error",
      "multi-or-nest"
    ],
    "dot-location": [
      "error",
      "property"
    ],
    "dot-notation": 2,
    "eqeqeq": [
      2,
      "smart"
    ],
    "id-length": 0,
    "ignoreUrls": true,
    "import/newline-after-import": 0,
    "import/no-unresolved": 0,
    "indent": [
      "error",
      "tab"
    ],
    "linebreak-style": [
      "error",
      "unix"
    ],
    "max-len": [
      "error",
      {
        "code": 120
      }
    ],
    "new-cap": [
      2,
      {
        "capIsNew": false
      }
    ],
    "no-alert": 0,
    "no-case-declarations": 2,
    "no-class-assign": 2,
    "no-compare-neg-zero": 2,
    "no-cond-assign": 2,
    "no-confusing-arrow": [
      "error",
      {
        "allowParens": true
      }
    ],
    "no-loops/no-loops": 2,
    "no-console": 1,
    "no-const-assign": 2,
    "no-constant-condition": 2,
    "no-control-regex": 2,
    "no-debugger": 2,
    "no-delete-var": 2,
    "no-dupe-args": 2,
    "no-dupe-class-members": 2,
    "no-dupe-keys": 2,
    "no-duplicate-case": 2,
    "no-empty": 2,
    "no-empty-character-class": 2,
    "no-empty-pattern": 2,
    "no-ex-assign": 2,
    "no-extra-boolean-cast": 2,
    "no-extra-semi": 2,
    "no-fallthrough": 2,
    "no-func-assign": 2,
    "no-global-assign": 2,
    "no-inner-declarations": 2,
    "no-invalid-regexp": 2,
    "no-irregular-whitespace": 2,
    "no-loop-func": 0,
    "no-mixed-spaces-and-tabs": 2,
    "no-new-symbol": 2,
    "no-obj-calls": 2,
    "no-octal": 2,
    "no-param-reassign": 0,
    "no-redeclare": 2,
    "no-regex-spaces": 2,
    "no-self-assign": 2,
    "no-shadow": 1,
    "no-sparse-arrays": 2,
    "no-template-curly-in-string": "error",
    "no-this-before-super": 2,
    "no-trailing-spaces": 2,
    "no-undef": 2,
    "no-underscore-dangle": [
      "error",
      {
        "allow": ["_id"],
        "allowAfterThis": true
      }
    ],
    "no-unexpected-multiline": 2,
    "no-unreachable": 2,
    "no-unsafe-finally": 2,
    "no-unsafe-negation": 2,
    "no-unused-labels": 2,
    "no-unused-vars": 2,
    "no-use-before-define": 2,
    "no-useless-call": 2,
    "no-useless-computed-key": 2,
    "no-useless-concat": 2,
    "no-useless-constructor": 2,
    "no-useless-escape": 1,
    "no-useless-rename": 2,
    "no-useless-return": 2,
    "object-curly-spacing": [
      "error",
      "always"
    ],
    "one-var-declaration-per-line": 2,
    "optimize-regex/optimize-regex": "warn",
    "prefer-arrow-callback": 2,
    "quotes": [
      "error",
      "single"
    ],
    "require-yield": 2,
    "semi": [
      "error",
      "never"
    ],
    "sort-imports": 2,
    "sort-keys": 2,
    "sort-vars": 2,
    "space-before-blocks": 2,
    "space-in-parens": [
      "error",
      "always"
    ],
    "space-infix-ops": 2,
    "spaced-comment": 2,
    "use-isnan": 2,
    "valid-typeof": 2
  }
}
