<form method="post">
  {% csrf_token %}
  <select name="student" required>
      {% for student in students %}
          <option value="{{ student.id }}" {% if initial_data.student == student.id|stringformat:"s" %}selected{% endif %}>
              {{ student.name }}
          </option>
      {% endfor %}
  </select>

  {% for question in page_obj %}
      <div class="question">
          <label for="question_{{ question.num_question }}">{{ question.text }}</label>
          <input type="number" 
                 name="question_{{ question.num_question }}" 
                 id="question_{{ question.num_question }}"
                 value="{{ initial_data.question_forloop.counter }}">
      </div>
  {% endfor %}

  <button type="submit">{% if page_obj.has_next %}Next{% else %}Submit{% endif %}</button>
</form>