module.exports = {
    content: [
        '../templates/**/*.html',
        '../../empleados/templates/**/*.html',
        '../../**/templates/**/*.html',
    ],
    theme: {
        extend: {},
    },
    plugins: [
        require('@tailwindcss/forms'),
        require('@tailwindcss/typography'),
        require('@tailwindcss/aspect-ratio'),
    ],
}