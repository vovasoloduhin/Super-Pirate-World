import pygame
import sys

class Button:
	def __init__(self, text, pos, action, font, width=250, height=60):
		self.text = text
		self.base_pos = pos
		self.pos = list(pos)
		self.target_x = pos[0]
		self.action = action
		self.font = font
		self.width = width
		self.height = height
		self.base_color = (100, 40, 40)
		self.hover_color = (160, 90, 40)
		self.text_color = (240, 220, 180)
		self.rect = pygame.Rect(0, 0, width, height)
		self.hovered = False

	def update(self):
		# Плавний перехід до target_x
		speed = 5  # чим більше — тим швидше
		if abs(self.pos[0] - self.target_x) > 1:
			self.pos[0] += (self.target_x - self.pos[0]) * speed * 0.1
		else:
			self.pos[0] = self.target_x

	def draw(self, surface):
		self.rect.center = (int(self.pos[0]), int(self.pos[1]))

		# Малюємо паралелограм
		color = self.hover_color if self.hovered else self.base_color
		points = [
			(self.rect.left + 20, self.rect.top),
			(self.rect.right, self.rect.top),
			(self.rect.right - 20, self.rect.bottom),
			(self.rect.left, self.rect.bottom)
		]
		pygame.draw.polygon(surface, color, points)

		# Текст
		text_surf = self.font.render(self.text, True, self.text_color)
		text_rect = text_surf.get_rect(center=self.rect.center)
		surface.blit(text_surf, text_rect)

	def check_hover(self, mouse_pos):
		was_hovered = self.hovered
		self.hovered = self.rect.collidepoint(mouse_pos)
		# Зміна цільової позиції для плавного руху
		self.target_x = self.base_pos[0] - 10 if self.hovered else self.base_pos[0]

	def check_click(self, mouse_pos):
		if self.rect.collidepoint(mouse_pos):
			self.action()


class Menu:
	def __init__(self, game):
		self.game = game
		self.font = pygame.font.Font(pygame.font.match_font('freesansbold'), 36)
		self.title_font = pygame.font.Font(pygame.font.match_font('freesansbold'), 60)
		self.buttons = [
			Button("Грати", (game.display_surface.get_width() // 2, 300), self.start_game, self.font),
			Button("Інструкція", (game.display_surface.get_width() // 2, 400), self.show_instructions, self.font),
			Button("Вийти", (game.display_surface.get_width() // 2, 500), self.quit_game, self.font),
		]

	def start_game(self):
		self.game.menu_active = False

	def show_instructions(self):
		self.instructions_screen()

	def quit_game(self):
		pygame.quit()
		sys.exit()

	def draw_background(self):
		width, height = self.game.display_surface.get_size()
		# Темний фентезі-градієнт
		for y in range(height):
			color = (
				10 + y // 10,
				10 + y // 20,
				20 + y // 30
			)
			pygame.draw.line(self.game.display_surface, color, (0, y), (width, y))

		# Додаткове затемнення
		overlay = pygame.Surface((width, height))
		overlay.set_alpha(90)
		overlay.fill((0, 0, 0))
		self.game.display_surface.blit(overlay, (0, 0))

	def instructions_screen(self):
		running = True
		back_button = Button("Назад", (self.game.display_surface.get_width() // 2, 650), lambda: None, self.font)

		while running:
			# Малюємо фон як у головному меню
			self.draw_background()

			# Заголовок
			title_surf = self.title_font.render("Інструкція", True, (255, 255, 255))
			title_rect = title_surf.get_rect(center=(self.game.display_surface.get_width() // 2, 100))
			self.game.display_surface.blit(title_surf, title_rect)

			# Текст інструкції
			instruction_lines = [
				"Управління: ",
				"A i D — рух",
				"Пробіл — стрибок",
				"E — атака",
				"",
				"Мета гри: ",
				"Збирайте монети й уникайте ворогів",
				"Дійдіть до прапора, щоб пройти рівень"
			]

			for i, line in enumerate(instruction_lines):
				line_surf = self.font.render(line, True, (200, 200, 220))
				line_rect = line_surf.get_rect(center=(self.game.display_surface.get_width() // 2, 180 + i * 50))
				self.game.display_surface.blit(line_surf, line_rect)

			# Кнопка "Назад"
			mouse_pos = pygame.mouse.get_pos()
			back_button.check_hover(mouse_pos)
			back_button.update()
			back_button.draw(self.game.display_surface)

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				if event.type == pygame.MOUSEBUTTONDOWN:
					if back_button.rect.collidepoint(mouse_pos):
						running = False
				if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
					running = False

			pygame.display.update()
			self.game.clock.tick(60)

	def run(self):
		self.draw_background()

		# Заголовок
		title_surf = self.title_font.render("Super Pirate World", True, (255, 215, 100))
		title_rect = title_surf.get_rect(center=(self.game.display_surface.get_width() // 2, 150))
		self.game.display_surface.blit(title_surf, title_rect)

		# Кнопки
		mouse_pos = pygame.mouse.get_pos()
		for button in self.buttons:
			button.check_hover(mouse_pos)
			button.update()
			button.draw(self.game.display_surface)

