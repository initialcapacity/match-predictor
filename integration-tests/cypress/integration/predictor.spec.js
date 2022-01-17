describe('match predictor', () => {
    it('loads the main page', () => {
        cy.visit('http://localhost:3010');

        cy.contains('Match Predictor').should('exist');

        cy.contains('Home').click().type('Chelsea')
        cy.contains('Away').click().type('Southampton')
        cy.contains('League').click().type('england')
        cy.contains('Season').click().clear().type('2020')

        cy.contains('Submit').click()

        cy.contains('HOME').should('exist')
    });
});
