import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import TaskCard from '../components/TaskCard.vue'
import type { Task } from '../services/api'

describe('TaskCard', () => {
  const mockTask: Task = {
    id: 1,
    url: 'https://www.instagram.com/reel/test',
    status: 'completed',
    transcript: 'Test transcript',
    error_message: null,
    language: 'en',
    topics: 'test, example',
    created_at: '2024-01-01T00:00:00Z',
    updated_at: '2024-01-01T00:00:00Z'
  }

  it('renders task information correctly', () => {
    const wrapper = mount(TaskCard, {
      props: { task: mockTask }
    })

    expect(wrapper.text()).toContain('#1')
    expect(wrapper.text()).toContain('COMPLETED')
    expect(wrapper.text()).toContain(mockTask.url)
  })

  it('shows view transcript button for completed tasks', () => {
    const wrapper = mount(TaskCard, {
      props: { task: mockTask }
    })

    const button = wrapper.find('.btn-primary')
    expect(button.exists()).toBe(true)
    expect(button.text()).toContain('View Transcript')
  })

  it('shows cancel button for pending tasks', () => {
    const pendingTask = { ...mockTask, status: 'pending' }
    const wrapper = mount(TaskCard, {
      props: { task: pendingTask }
    })

    const button = wrapper.find('.btn-danger')
    expect(button.exists()).toBe(true)
    expect(button.text()).toContain('Cancel')
  })

  it('emits view-transcript event when button clicked', async () => {
    const wrapper = mount(TaskCard, {
      props: { task: mockTask }
    })

    await wrapper.find('.btn-primary').trigger('click')
    expect(wrapper.emitted('viewTranscript')).toBeTruthy()
    expect(wrapper.emitted('viewTranscript')?.[0]).toEqual([1])
  })
})
