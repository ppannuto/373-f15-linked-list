#include <stdio.h>
#include <stdlib.h>

#include "list.h"
#include "print_list.h"

int main() {
	printf("@@ START\n");

	list_t* head = malloc(sizeof(list_t));
	head->index = 1;

	head->next = malloc(sizeof(list_t));
	head->next->index = 5;

	head->next->next = malloc(sizeof(list_t));
	head->next->next->index = 9;

	head->next->next->next = NULL;

	print_list(head);

	unsigned i;
	for (i=0; i<=12; i+=4) {
		list_t* new_element = malloc(sizeof(list_t));
		new_element->index = i;
		head = insert_sorted(head, new_element);
		print_list(head);
	}

	head = reverse(head);
	print_list(head);

	printf("@@ END\n");
	return 0;
}

