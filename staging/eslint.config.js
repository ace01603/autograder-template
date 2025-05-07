import { defineConfig } from "eslint/config";
import js from "@eslint/js";

export default defineConfig([
	{
		files: ["**/*.js"],
		plugins: {
			js,
		},
		extends: ["js/recommended"],
        rules: {
			"no-unused-vars": "off",
            "no-undef": "off",
            "camelcase": "error",
            "consistent-return": "error",
            "eqeqeq": "error",
            "no-var": "error"
		},
	},
]);
