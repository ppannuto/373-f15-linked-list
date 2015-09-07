#include <assert.h>
#include <stdlib.h>

#include "list.h"

// Takes a valid, sorted list starting at `head` and adds the element
// `new_element` to the list. The list is sorted based on the value of the
// `index` member in ascending order. Returns a pointer to the head of the list
// after the insertion of the new element.
list_t* insert_sorted(list_t* head, list_t* new_element) {
	assert(head != NULL);
	assert(new_element != NULL);

	if (new_element->index <= head->index) {
		new_element->next = head;
		return new_element;
	}

	list_t* current = head;
	while (current->next != NULL) {
		if (new_element->index <= current->next->index) {
			new_element->next = current->next;
			current->next = new_element;
			return head;
		}
		current = current->next;
	}

	current->next = new_element;
	new_element->next = NULL;
	return head;
}

list_t* reverse_internal(list_t* current, list_t* current_next) {
	if (current_next == NULL) {
		return current;
	}

	list_t* new_head;
	new_head = reverse_internal(current_next, current_next->next);
	current_next->next = current;
	return new_head;
}

// Reverses the order of the list starting at `head` and returns a pointer to
// the resulting list. You do not need to preserve the original list.
list_t* reverse(list_t* head) {
	assert(head != NULL);

	// (Ab)use the stack to not deal with dynamic memory
	list_t* new_head;
	new_head = reverse_internal(head, head->next);
	head->next = NULL;
	return new_head;
}

