#include <stdio.h>
#include <assert.h>

#include "print_list.h"

void print_list(list_t* head) {
	assert(head != NULL);

	static unsigned count = 0;
	printf("@@ PRINT %u\n", count++);

	do {
		printf("%u -> ", head->index);
		head = head->next;
	} while (head);
	printf("nil\n");
}
