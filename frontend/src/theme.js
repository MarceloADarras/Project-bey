import { ref } from 'vue'

const currentTheme = ref(localStorage.getItem('theme') || 'light')

export function useTheme() {
  const setTheme = (newTheme) => {
    currentTheme.value = newTheme
    localStorage.setItem('theme', newTheme)
    if (newTheme === 'dark') {
      document.documentElement.classList.add('dark')
    } else {
      document.documentElement.classList.remove('dark')
    }
  }

  const initTheme = () => {
    setTheme(currentTheme.value)
  }

  return {
    theme: currentTheme,
    setTheme,
    initTheme
  }
}
